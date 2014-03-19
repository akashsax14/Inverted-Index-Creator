/*
This parser is not authored by me. It has been created and written by "Xiaohui Long".
I have only used it for parsing web pages in my code
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <locale.h>


#define PTAG_B	1
#define PTAG_I	2
#define	PTAG_H	3
#define PTAG_TITLE	4
#define PTAG_SCRIPT	5

#define _TITLE_TAG	0x0001
#define _B_TAG		0x0004
#define _H_TAG		0x0008
#define _I_TAG		0x0010
#define strnicmp strncasecmp
#define xl_isascii(c) (((c) >= 0) && ((c) <= 255))
#define xl_isdigit(c) (((c) >= '0') && ((c) <= '9'))
#define xl_islower(c) (((c) >= 'a') && ((c) <= 'z'))
#define xl_isupper(c) (((c) >= 'A') && ((c) <= 'Z'))
#define xl_isindexable(c) (xl_isdigit(c) || xl_islower(c) || xl_isupper(c))
#define xl_tolower(c) ((c) += 'a' - 'A')
#define isascii xl_isascii

char* parser_init(char* doc)
{
	char *p;

	if (strnicmp(doc, "HTTP/", 5))
		return NULL;
	
	for (p = doc; (*p != ' ')&&(*p); p++);
	if (*p == '\0')
		return NULL;

	if (atoi(p) != 200)
		return NULL;

	p = strstr(p,  "\r\n\r\n");
	if (p == NULL)
		return NULL;

	return p+4;
}

int tag_parser(char* tag, int len, char* back_tag)
{
	int i = 0;

	if (tag[0] == '/')
	{
		*back_tag = 1;
		i++;

	} else
		*back_tag = 0;

	switch (tag[i])
	{
	case 'b':
	case 'B':
	case 'i':
	case 'I':
		if (!isascii(tag[i+1]))
			return 0;
		if (!isspace(tag[i+1]))
			return 0;
		if ((tag[i] == 'b') || (tag[i] == 'B'))
			return PTAG_B;
		return PTAG_I;

	case 'e':
	case 'E':
		i++;
		if (!isascii(tag[i+1]))
			return 0;

		if (((tag[i]=='m')||(tag[i]=='M')) && (isspace(tag[i+1])))
			return PTAG_I;
		return 0;
	
	case 'h':
	case 'H':
		i++;
		if (!isascii(tag[i+1]))
			return 0;

		if (((tag[i]>='1')&&(tag[i]<='6')) && (isspace(tag[i+1])))
			return PTAG_H;
		return 0;
	
	case 't':
	case 'T':
		i++;
		if (!isascii(tag[i+4]))
			return 0;
		if ((0==strnicmp(tag+i, "itle", 4)) && (isspace(tag[i+4])))
			return PTAG_TITLE;
		return 0;
	
	case 's':
	case 'S':
		i++;
		if (!isascii(tag[i+5]))
			return 0;
		if ((0==strnicmp(tag+i, "trong", 5)) && (isspace(tag[i+5])))
			return PTAG_B;
		if ((0==strnicmp(tag+i, "cript", 5)) && (isspace(tag[i+5])))
			return PTAG_SCRIPT;
		return 0;

	default:
		break;
	}

	return 0;
}

#define xlbit_set(__b1, __b2)	((__b1) |= (__b2))
#define xlbit_unset(__b1, __b2)	((__b1) &= ~(__b2))
#define xlbit_check(__b1, __b2) ((__b1)&(__b2))

int parser(char* url, char* doc, char* buf, int blen, int maxlen)
{
	char *p, *purl, *word, *ptag, *pbuf;
	char ch, back_tag, intag, inscript;
	unsigned tag_flag;
	int ret;

	p = parser_init(doc);
	if (p == NULL)
		return 0;
	pbuf = buf;

/* parsing URL */
	purl = url;
	while (*purl != '\0')
	{
		if (!xl_isindexable(*purl))
		{
			purl++;
			continue;
		}

		word = purl;
		while (xl_isindexable(*purl))
		{
			if (xl_isupper(*purl))
				xl_tolower(*purl);
			purl++;
		}

		ch = *purl;
		*purl = '\0';

		if (pbuf-buf+purl-word+3 > blen-1)
			return -1;
		sprintf(pbuf, "%s U\n", word);
		pbuf += (purl-word)+3;

		*purl = ch;
	}

/* parsing page */
	tag_flag = 0;
	intag = 0;
	inscript = 0;

	while ((p - doc) < maxlen)
	{
		if(*p == '&' && *(p+1)=='n' && *(p+2)=='b' && *(p+3)=='s' && *(p+4)=='p')
		{
			p += 5;
			continue;
		}
		if (!xl_isindexable(*p))
		{
			if (*p != '>' )
			{
				if (*p == '<')
				{
					ptag = p;
					intag = 1;
				}
				p++;
				continue;
			}

			if (intag == 0)
			{
				p++;
				continue;
			}

			*p = ' ';
			ret = tag_parser(ptag+1, p-ptag, &back_tag);
			switch (ret)
			{
				case PTAG_B:

					if (back_tag == 0)
						xlbit_set(tag_flag, _B_TAG);
					else
						xlbit_unset(tag_flag, _B_TAG);
					break;

				case PTAG_I:

					if (back_tag == 0)
						xlbit_set(tag_flag, _I_TAG);
					else
						xlbit_unset(tag_flag, _I_TAG);
					break;

				case PTAG_H:

				if (back_tag == 0)
					xlbit_set(tag_flag, _H_TAG);
				else
					xlbit_unset(tag_flag, _H_TAG);
				break;

				case PTAG_TITLE:

					if (back_tag == 0)
						xlbit_set(tag_flag, _TITLE_TAG);
					else
						xlbit_unset(tag_flag, _TITLE_TAG);
					break;

				case PTAG_SCRIPT:

					if (back_tag == 0)
						inscript = 1;
					else
						inscript = 0;

				default:
					break;
			}

			intag = 0;
			p++;
			continue;
		}

		if (inscript || intag)
		{
			p++;
			continue;
		}

		word = p;
		while (xl_isindexable(*p))
		{
			if (xl_isupper(*p))
				xl_tolower(*p);
			p++;
		}

		ch = *p;
		*p = '\0';

		if (pbuf-buf+p-word+1 > blen-1)
			return -1;
		sprintf(pbuf, "%s ", word);
		pbuf += (p-word)+1;

		if (xlbit_check(tag_flag, _B_TAG))
		{
			if (pbuf-buf+1> blen-1)
				return -1;
			*pbuf = 'B';
			pbuf++;
		}

		if (xlbit_check(tag_flag, _H_TAG))
		{
			if (pbuf-buf+1> blen-1)
				return -1;
			*pbuf = 'H';
			pbuf++;
		}

		if (xlbit_check(tag_flag, _I_TAG))
		{
			if (pbuf-buf+1> blen-1)
				return -1;
			*pbuf = 'I';
			pbuf++;
		}

		if (xlbit_check(tag_flag, _TITLE_TAG))
		{
			if (pbuf-buf+1> blen-1)
				return -1;
			*pbuf = 'T';
			pbuf++;
		}

		if (tag_flag == 0)
		{
			if (pbuf-buf+1> blen-1)
				return -1;
			*pbuf = 'P';
			pbuf++;
		}

		if (pbuf-buf+1> blen-1)
			return -1;

		*pbuf = '\n';
		pbuf++;
		*p = ch;
	}

	*pbuf = '\0';
	return pbuf-buf;
}
