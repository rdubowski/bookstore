import React from 'react'
import {Pagination} from 'react-bootstrap'
import {LinkContainer} from 'react-router-bootstrap'

function Paginate({pages, page, keyword = '', isAdmin = false}) {
    if (keyword) {
        keyword = keyword.split('?keyword=')[1].split('&')[0]
    }
    return (
        pages > 1 && (
            <Pagination>
                {[...Array(pages).keys()].map((actPage) => (
                    <LinkContainer
                        key={actPage + 1}
                        to={!isAdmin ? `/?keyword=${keyword}&page=${actPage + 1}`
                            : `/admin/books/?keyword=${keyword}&page=${actPage + 1}`
                        }
                    >
                        <Pagination.Item active={actPage + 1 === page}>{actPage + 1}</Pagination.Item>
                    </LinkContainer>
                ))}
            </Pagination>
        )
    )
}

export default Paginate;