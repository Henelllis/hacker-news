import React, {Component} from 'react';
import Link from'./Link';
import { Query } from 'react-apollo'
import gql from 'graphql-tag'

const FEED_QUERY = gql`
  {
    feed {
      links {
        id
        createdAt
        url
        description
      }
    }
  }
`

class LinkList extends Component{
    render(){
        const linksToRender = [
            {
                id: '1',
                description: 'Prisma turns your database into a GraphQL API 😎 😎',
                url: 'https://prismagraphql.com',
            },
            {
                id:'2',
                description: 'The Best GraphQl Client',
                url: 'https://www.apollographql.com/docs/react/',
            },
        ]

        return(
            <Query query={FEED_QUERY}>
                {({ loading, error, data}) => {
                    if(loading) return<div> LOADING </div>
                    if(error) return <div> ERROR </div>

                    const linksToRender = data.feed.links

                    return(
                        <div>
                            {linksToRender.map(link => <Link key={link.id} link={link} />)}
                        </div>
                    )
                }}

            </Query>
        )
    }
}

export default LinkList